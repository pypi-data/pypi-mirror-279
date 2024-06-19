use pyo3::prelude::*;
use validator::ValidateEmail;

#[pyfunction]
fn validate(email: String) -> PyResult<bool> {
    Ok(email.validate_email())
}

#[pymodule]
fn _email_validator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(validate, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use pyo3::types::IntoPyDict;

    use super::*;

    #[test]
    fn test_valid_email() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let email_validator = PyModule::new_bound(py, "_email_validator").unwrap();
            _email_validator(&email_validator).unwrap();

            let locals = [("email_validator", email_validator)].into_py_dict_bound(py);
            let result: bool = py
                .eval_bound(
                    "email_validator.validate('example@example.com')",
                    None,
                    Some(&locals),
                )
                .unwrap()
                .extract()
                .unwrap();
            assert!(result);
        });
    }

    #[test]
    fn test_invalid_email() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let email_validator = PyModule::new_bound(py, "_email_validator").unwrap();
            _email_validator(&email_validator).unwrap();

            let locals = [("email_validator", email_validator)].into_py_dict_bound(py);
            let result: bool = py
                .eval_bound(
                    "email_validator.validate('invalid-email')",
                    None,
                    Some(&locals),
                )
                .unwrap()
                .extract()
                .unwrap();
            assert!(!result);
        });
    }
}
