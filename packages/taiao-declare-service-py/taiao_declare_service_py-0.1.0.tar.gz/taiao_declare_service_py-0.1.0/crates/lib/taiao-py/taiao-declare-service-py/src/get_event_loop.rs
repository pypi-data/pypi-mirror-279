use pyo3::{PyAny, PyResult, Python};

pub fn get_event_loop(py: Python) -> PyResult<&PyAny> {
    let asyncio = py.import("asyncio")?;
    let get_event_loop = asyncio.getattr("get_event_loop")?;
    get_event_loop.call0()
}
