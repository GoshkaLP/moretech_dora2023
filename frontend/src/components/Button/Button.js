import './Button.css';

function Button(props) {
  const { type, text, icon } = props;

  return (
    <div className={ `button${ type ? ` button_type_${ type }` : "" }` }>
      { text && <p className="button__text">{ text }</p> }
      { icon && <img className="button__icon" src={ icon } alt="" /> }
    </div>
  )
}

export default Button;