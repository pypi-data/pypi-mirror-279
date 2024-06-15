#[macro_export]
macro_rules! create_action_enum {
    ($name: ident, $rust_type: ty, $python_type: ty) => {
        /// Represents an action by a participant in the protocol.
        ///
        /// The basic flow is that each participant receives messages from other participants,
        /// and then reacts with some kind of action.
        ///
        /// This action can consist of sending a message, doing nothing, etc.
        ///
        /// Eventually, the participant returns a value, ending the protocol.
        #[pyclass]
        #[derive(Debug, Clone)]
        pub enum $name {
            Wait {},
            SendMany {
                message_data: MessageData,
            },
            SendPrivate {
                participant: PyParticipant,
                message_data: MessageData,
            },
            Return {
                result: $python_type,
            },
        }

        impl From<Action<$rust_type>> for $name {
            fn from(value: Action<$rust_type>) -> Self {
                match value {
                    Action::Wait => $name::Wait {},
                    Action::SendMany(data) => $name::SendMany { message_data: data },
                    Action::SendPrivate(participant, data) => $name::SendPrivate {
                        participant: participant.into(),
                        message_data: data,
                    },
                    Action::Return(result) => $name::Return {
                        result: result.into(),
                    },
                }
            }
        }
    };
}
