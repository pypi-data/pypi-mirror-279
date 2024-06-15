use pyo3::prelude::*;
use pyo3::types::PyModule;

mod action;
mod arithmetic;
mod keyshare;
mod participant;
mod presign;
mod protocol;
mod sign;
mod triples;

#[pymodule]
fn cait_sith(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // participant
    m.add_class::<participant::PyParticipant>()?;

    // keyshare
    m.add_function(wrap_pyfunction!(keyshare::py_keygen, m)?)?;
    m.add_class::<keyshare::PyKeygenOutput>()?;
    m.add_class::<keyshare::KeygenAction>()?;
    m.add_class::<keyshare::KeygenProtocol>()?;

    // triples
    m.add_function(wrap_pyfunction!(triples::py_generate_triple_many, m)?)?;
    m.add_class::<triples::PyTripleGenerationOutput>()?;
    m.add_class::<triples::PyTripleShare>()?;
    m.add_class::<triples::TripleGenerationActionMany>()?;
    m.add_class::<triples::TripleGenerationProtocolMany>()?;

    // presign
    m.add_function(wrap_pyfunction!(presign::py_presign, m)?)?;
    m.add_class::<presign::PyPresignArguments>()?;
    m.add_class::<presign::PyPresignOutput>()?;
    m.add_class::<presign::PresignGenerationAction>()?;
    m.add_class::<presign::PresignGenerationProtocol>()?;

    // sign
    m.add_function(wrap_pyfunction!(sign::py_sign, m)?)?;
    m.add_function(wrap_pyfunction!(sign::py_verify, m)?)?;
    m.add_class::<sign::PyFullSignature>()?;
    m.add_class::<sign::SignAction>()?;
    m.add_class::<sign::SignAction>()?;

    // auxiliary
    m.add_function(wrap_pyfunction!(arithmetic::lagrange_calculation, m)?)?;
    m.add_function(wrap_pyfunction!(arithmetic::multiply_by_generator, m)?)?;
    m.add_function(wrap_pyfunction!(arithmetic::multiply_two_points, m)?)?;
    m.add_function(wrap_pyfunction!(arithmetic::invert, m)?)?;

    Ok(())
}
