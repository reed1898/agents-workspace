'use client';

import { useEffect } from 'react';
import { buildPageTitle } from './page-titles';

export const usePageTitle = (title?: string) => {
  useEffect(() => {
    document.title = buildPageTitle(title);
  }, [title]);
};
