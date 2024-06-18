use std::panic::panic_any;
use std::sync::{Mutex, PoisonError};
use pyo3::{PyAny, pyfunction, PyResult};
use pyo3::exceptions::PySystemExit;
use taiao_py_utils::FromStrParameter;
use taiao_service_result::ServiceCompletion;
use taiao_storage_py::OwnedStorageType;
use taiao_types_py::{ClientName, Periodicity, PortNumber, Privacy, ProjectName, ServiceName};
use crate::get_event_loop::get_event_loop;
use crate::python_service_main::python_service_main;

type OrStringRepr<T> = FromStrParameter<false, T>;

/// Formats the sum of two numbers as string.
#[pyfunction]
pub fn declare_service(
    client: OrStringRepr<ClientName>,
    project: OrStringRepr<ProjectName>,
    service: OrStringRepr<ServiceName>,
    storage: &OwnedStorageType,
    body: &PyAny,
    privacy: Privacy,
    periodicity: Periodicity,
    listen: OrStringRepr<PortNumber>
) -> PyResult<()> {
    
    let event_loop = get_event_loop(body.py())?;
    
    let service_main = python_service_main(
        event_loop,
        client.value,
        project.value,
        service.value,
        storage,
        body,
        privacy,
        periodicity,
        listen.value
    )?;
    
    let async_main = move || async { 
        let handle = std::thread::spawn(service_main);
        match handle.join() {
            Ok(result) => Ok(result.map_err(Mutex::new)), // pyo3_asyncio::tokio::run has unnecessary Sync bound
            Err(error) => panic_any(error)
        }
    };

    let result = pyo3_asyncio::tokio::run_until_complete(event_loop, async_main())?;

    let exit = match result {
        Ok(completion) => PySystemExit::new_err(
            match completion {
                ServiceCompletion::Finished => ServiceCompletion::FINISHED_EXIT_CODE,
                ServiceCompletion::FinishedForNow => ServiceCompletion::FINISHED_FOR_NOW_EXIT_CODE
            }
        ),
        Err(error) => { 
            let error = error.into_inner().unwrap_or_else(PoisonError::into_inner);
            PySystemExit::new_err(error.to_string()) 
        }
    };
    
    Err(exit)
}