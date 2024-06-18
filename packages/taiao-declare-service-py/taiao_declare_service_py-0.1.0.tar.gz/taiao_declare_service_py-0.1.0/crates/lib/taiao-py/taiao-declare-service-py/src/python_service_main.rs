use std::ops::Deref;
use pyo3::{IntoPy, PyAny, PyResult};
use pyo3_asyncio::TaskLocals;
use taiao_declare_service_macro::reexport::taiao_error::DynTAIAOError;
use taiao_service_py::PythonService;
use taiao_storage::impls::NoStorage;
use taiao_storage_py::{OwnedStorageType, OwnedStorageTypeInner};
use taiao_service_result::ServiceCompletion;
use taiao_storage::impls::stream::OwnedStream;
use taiao_storage_py::record::{Record};
use taiao_types_py::{ClientName, Periodicity, PortNumber, Privacy, ProjectName, ServiceName};

#[inline]
pub fn python_service_main(
    event_loop: &PyAny,
    client: ClientName,
    project: ProjectName,
    service: ServiceName,
    storage: &OwnedStorageType,
    body: &PyAny,
    privacy: Privacy,
    periodicity: Periodicity,
    listen: PortNumber
) -> PyResult<impl FnOnce() -> Result<ServiceCompletion, DynTAIAOError>> {
    let py = body.py();

    let locals = TaskLocals::new(event_loop);
    
    let storage = storage.deref().map_ref(|schema| 
        schema.as_ref(py).get().deref().clone()
    );
    
    let body = body.into_py(py);

    let service_main = move || {
        let storage_type = storage.as_storage();
        match storage {
            OwnedStorageTypeInner::NoStorage => taiao_declare_service_macro::declare_service!(
                    @service_main_impl
                    client=client,
                    project=project,
                    service=service,
                    storage=storage_type,
                    body=PythonService::<NoStorage>::new(body, locals),
                    privacy=privacy,
                    interval=periodicity,
                    listen=listen
                ),
            OwnedStorageTypeInner::Stream { state_schema, output_schema } => taiao_declare_service_macro::declare_service!(
                    @service_main_impl
                    client=client,
                    project=project,
                    service=service,
                    storage=storage_type,
                    body=PythonService::<OwnedStream<Record, Record>>::new(body, locals),
                    privacy=privacy,
                    interval=periodicity,
                    listen=listen,
                    storage-init=(state_schema, output_schema)
                )
        }
    };
    
    Ok(service_main)
}