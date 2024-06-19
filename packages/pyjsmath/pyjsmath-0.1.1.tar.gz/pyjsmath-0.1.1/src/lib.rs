use pyo3::prelude::*;

#[pyfunction]
pub fn add(left: f64, right: f64) -> PyResult<f64> {
    Ok(left + right)
}

#[pyfunction]
pub fn sub(left: f64, right: f64) -> PyResult<f64> {
    Ok(left - right)
}

#[pyfunction]
pub fn mul(left: f64, right: f64) -> PyResult<f64> {
    Ok(left * right)
}

#[pyfunction]
pub fn truediv(left: f64, right: f64) -> PyResult<i64> {
    Ok((left / right) as i64)
}

#[pyfunction]
pub fn floordiv(left: f64, right: f64) -> PyResult<f64> {
    Ok(left / right)
}

#[pyfunction]
pub fn modulo(left: f64, right: f64) -> PyResult<f64> {
    Ok(left % right)
}

#[pyfunction]
pub fn pow(left: f64, right: f64) -> PyResult<f64> {
    Ok(left.powf(right))
}

#[pymodule]
fn pyjsmath(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(sub, m)?)?;
    m.add_function(wrap_pyfunction!(mul, m)?)?;
    m.add_function(wrap_pyfunction!(truediv, m)?)?;
    m.add_function(wrap_pyfunction!(floordiv, m)?)?;
    m.add_function(wrap_pyfunction!(modulo, m)?)?;
    m.add_function(wrap_pyfunction!(pow, m)?)?;
    Ok(())
}
