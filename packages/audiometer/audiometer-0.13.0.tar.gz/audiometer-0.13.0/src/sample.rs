use pyo3::prelude::*;
use pyo3::types::PyBytes;

// Return PyBytes: https://users.rust-lang.org/t/pyo3-best-way-to-return-bytes-from-function-call/46577/2
// NOTE: `Vec<u8>`을 리턴하는 것보다 `PyBytes`를 리턴하는 것이 빠름
#[pyfunction]
pub fn convert_24bit_to_32bit(py: Python, data: &PyBytes) -> PyObject {
    let len_data = data.len().unwrap();
    let data_bytes = data.as_bytes();
    let mut result = Vec::with_capacity(len_data / 3 * 4);

    data_bytes.chunks(3).for_each(|chunk| {
        let mut samples = [0u8; 4];
        let b2 = chunk[2];
        samples[0] = if b2 > 0x7f { 0xff } else { 0x00 };
        samples[1] = chunk[0];
        samples[2] = chunk[1];
        samples[3] = b2;
        result.extend_from_slice(&samples);
    });

    PyBytes::new(py, &result).into()
}
