const MINUTE = 60;
const HOUR = MINUTE * 60;
const DAY = HOUR * 24;
const WEEK = DAY * 7;

// type types = "minute" | "hour" | "day" | "week";
export function getTimeUnits(time: number) {
  let timeLeft = time;
  const date = {
    seconds: 0,
    minutes: 0,
    hours: 0,
    days: 0,
    weeks: 0,
  };

  const weeks = Math.floor(timeLeft / WEEK);
  if (weeks) {
    date.weeks = weeks;
    timeLeft -= weeks * WEEK;
  }
  const days = Math.floor(timeLeft / DAY);
  if (days) {
    date.days = days;
    timeLeft -= days * DAY;
  }
  const hours = Math.floor(timeLeft / HOUR);
  if (hours) {
    date.hours = hours;
    timeLeft -= hours * HOUR;
  }
  const minutes = Math.floor(timeLeft / MINUTE);
  if (minutes) {
    date.minutes = minutes;
    timeLeft -= minutes * MINUTE;
  }

  date.seconds = timeLeft;
  return date;
}

export function formatTime(time: number) {
  const { weeks, days, hours, minutes, seconds } = getTimeUnits(time);
  const totalHours = weeks * 7 * 24 + days * 24 + hours;
  return `${totalHours < 10 ? "0" + totalHours : totalHours}:${
    minutes < 10 ? "0" + minutes : minutes
  }:${seconds < 10 ? "0" + seconds : seconds}`;
}
