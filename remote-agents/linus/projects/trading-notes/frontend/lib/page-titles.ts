export const APP_TITLE = 'Trading Notes';

export const buildPageTitle = (title?: string) => {
  if (!title) return APP_TITLE;
  return `${title} - ${APP_TITLE}`;
};
