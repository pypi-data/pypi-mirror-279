use pyo3::prelude::*;

mod declare_service;
mod get_event_loop;
mod python_service_main;

/// A Python module implemented in Rust.
#[pymodule]
fn taiao_declare_service_py(_py: Python, m: &PyModule) -> PyResult<()> {
    pub use taiao_py_utils::add_package_submodule;
    m.add_function(wrap_pyfunction!(declare_service::declare_service, m)?)?;
    add_package_submodule(m, "types", taiao_types_py::taiao_types_py)?;
    add_package_submodule(m, "service_result", taiao_service_result_py::taiao_service_result_py)?;
    add_package_submodule(m, "storage", taiao_storage_py::taiao_storage_py)?;
    Ok(())
}
