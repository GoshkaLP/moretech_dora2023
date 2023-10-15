import logo from '../../images/logo.svg';
import infoIcon from '../../images/info-icon.svg';
import './Header.css';

function Header(props) {
  const { info } = props;

  return (
    <div className="header">
      <img src={ logo } className="header__logo" alt="ВТБ" />
      { info &&
        <div className="header__info">
          <p className="header__info-text" style={{ color: info.color }}>{ info.text }</p>
          <img className="header__info-icon" style={{ fill: info.color }} src={ infoIcon } alt="" />
        </div>
      }
    </div>
  );
}

export default Header;