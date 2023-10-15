import "./Message.css";

function Message(props) {
  const { text = "...", type = "outgoing" } = props;

  return (
    <div className={`message message_type_${type}`}>
      {type === "incoming" &&
        <p className="message__author">Ассистент</p>
      }
      <p className={`message__text message__text_type_${type}`}>{text}</p>
    </div>
  );
}

export default Message;
