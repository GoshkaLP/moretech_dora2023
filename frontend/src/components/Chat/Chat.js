import { Link } from 'react-router-dom';
import Button from '../Button/Button';
import Message from '../Message/Message';
import chatIcon from '../../images/chat-icon.svg';
import stub from '../../images/stub.svg';
import './Chat.css';

function Chat() {

  

  return (
    <div className="chat">
      <div className="chat__header">
        <a href="/" className="chat__header-link">Вернуться к карте</a>
      </div>
      <div className="chat__message-list">
        <Message text="Добро пожаловать!" type="incoming" />
        <Message text="Какие услуги вас интересуют?" type="incoming" />
        <Message text="Для физлиц" />
        <Message text="Отлично. Чем займемся сегодня?" type="incoming" />
        <Message text="Консультация по инвестиционным продуктам, открытие сейфового ящика" />
        <Message text="Последний вопрос. Откуда отправляемся?" type="incoming" />
        <img className="chat__stub" src={ stub } alt="" />
      </div>
      <Link to="/best-route" style={{ color: "none", textDecoration: "none" }}>
        <Button text="Ответить" icon={ chatIcon } />
      </Link>
    </div>
  );
}

export default Chat;