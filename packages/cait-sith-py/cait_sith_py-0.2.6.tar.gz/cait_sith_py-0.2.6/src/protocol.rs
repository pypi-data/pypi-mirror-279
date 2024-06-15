#[macro_export]
macro_rules! create_protocol {
    ($name: ident, $rust_output_type: ty, $py_action_type: ty) => {
        /// A trait for protocols.
        ///
        /// Basically, this represents a struct for the behavior of a single participant
        /// in a protocol. The idea is that the computation of that participant is driven
        /// mainly by receiving messages from other participants.
        #[pyclass]
        pub struct $name {
            protocol: Arc<Mutex<dyn Protocol<Output = $rust_output_type>>>,
        }

        // TODO: perhaps, in some cases, it's better to drop Arc<Mutex>,
        //  e.g. when we know for a fact presence of exclusiveness of an ownership
        unsafe impl Send for $name {}

        #[pymethods]
        impl $name {
            /// Poke the protocol, receiving a new action.
            ///
            /// The idea is that the protocol should be poked until it returns an error,
            /// or it returns an action with a return value, or it returns a wait action.
            ///
            /// Upon returning a wait action, that protocol will not advance any further
            /// until a new message arrives.
            fn poke(&mut self) -> PyResult<$py_action_type> {
                let mut protocol_guard = self.protocol.lock().unwrap();
                let poke_result = protocol_guard.poke().unwrap();
                Ok(poke_result.into())
            }

            /// Inform the protocol of a new message.
            fn message(&mut self, from: PyParticipant, data: MessageData) {
                let mut protocol_guard = self.protocol.lock().unwrap();
                protocol_guard.message(from.into(), data)
            }
        }
    };
}
