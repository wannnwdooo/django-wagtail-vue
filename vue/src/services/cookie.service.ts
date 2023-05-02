const getCookie = (name: string): string | undefined => {
  const cookies = document.cookie.split("; ");
  for (const cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split("=");
    if (cookieName === name) {
      return decodeURIComponent(cookieValue);
    }
  }
  return undefined;
};

const setCookie = (
  name: string,
  value: string,
  options: { [key: string]: any } = {}
): void => {
  let cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
  for (const optionName in options) {
    const optionValue = options[optionName];
    if (optionValue === true) {
      cookie += `; ${optionName}`;
    } else {
      cookie += `; ${optionName}=${optionValue}`;
    }
  }
  document.cookie = cookie;
};

const cookieService = {
  get: getCookie,
  set: setCookie
};
export default cookieService
