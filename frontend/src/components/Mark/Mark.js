import lowPoularityIcon from "../../images/low-popularity-icon.svg";
import mediumPoularityIcon from "../../images/medium-popularity-icon.svg";
import highPoularityIcon from "../../images/high-popularity-icon.svg";

import "./Mark.css";

function Mark(props) {
  const { percentage } = props;

  const deg = 360 * percentage / 100 + 180
  let popularity;
  if (percentage >= 70) {
    popularity = "high";
  } else if (percentage >= 35) {
    popularity = "medium";
  } else {
    popularity = "low";
  }

  return (
    <div className="mark">

      <div class="progress-circle">
        <div class="left-half-clipper">
            <div class="first50-bar"></div>
            <div class="value-bar"></div>
        </div>
      </div>

      <div className="mark__internals">
        {popularity === "high" && (
          <img
            className="mark__icon mark__icon_color_red"
            src={highPoularityIcon}
            alt=""
          />
        )}
        {popularity === "medium" && (
          <img
            className="mark__icon mark__icon_color_yellow"
            src={mediumPoularityIcon}
            alt=""
          />
        )}
        {popularity === "low" && (
          <img
            className="mark__icon mark__icon_color_green"
            src={lowPoularityIcon}
            alt=""
          />
        )}
      </div>
    </div>
  );
}

export default Mark;
