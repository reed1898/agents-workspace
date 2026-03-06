import type { AccountType } from '@/lib/types/account';

export function parseNumber(value: unknown): number | null {
  if (value === null || value === undefined) return 0;
  const normalized = String(value).trim();
  if (normalized === '') return 0;
  const parsed = Number.parseFloat(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

export function getCurrencySymbol(accountType?: AccountType): string {
  const currencyMap: Record<AccountType, string> = {
    us_stock: '$',
    crypto: '$',
    a_stock: '¥',
    hk_stock: 'HK$',
  };
  return (accountType && currencyMap[accountType]) || '$';
}

export function formatGroupedNumber(value: unknown, fractionDigits: number): string {
  const parsed = parseNumber(value);
  if (parsed === null) return String(value ?? '');
  return new Intl.NumberFormat('zh-CN', {
    useGrouping: true,
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  }).format(parsed);
}

export function formatFixedNumber(value: unknown, fractionDigits: number): string {
  const parsed = parseNumber(value);
  if (parsed === null) return String(value ?? '');
  return parsed.toFixed(fractionDigits);
}

export function formatNumber(
  value: unknown,
  options: {
    minimumFractionDigits?: number;
    maximumFractionDigits: number;
    locale?: string;
  }
): string {
  const parsed = parseNumber(value);
  if (parsed === null) return String(value ?? '');
  const minimumFractionDigits = options.minimumFractionDigits ?? 0;
  const maximumFractionDigits = options.maximumFractionDigits;
  return new Intl.NumberFormat(options.locale ?? 'en-US', {
    useGrouping: true,
    minimumFractionDigits,
    maximumFractionDigits,
  }).format(parsed);
}

export function formatMoney(
  value: unknown,
  options?: { accountType?: AccountType; fallbackFractionDigits?: number }
): string {
  const parsed = parseNumber(value);
  if (parsed === null) return String(value ?? '');

  const symbol = getCurrencySymbol(options?.accountType);
  const fallbackFractionDigits = options?.fallbackFractionDigits ?? 2;
  const formatted = new Intl.NumberFormat('en-US', {
    useGrouping: true,
    minimumFractionDigits: fallbackFractionDigits,
    maximumFractionDigits: fallbackFractionDigits,
  }).format(parsed);
  return `${symbol}${formatted}`;
}

function formatCryptoPrice(value: number): string {
  const sign = value < 0 ? '-' : '';
  const absValue = Math.abs(value);

  if (absValue >= 1) {
    return new Intl.NumberFormat('en-US', {
      useGrouping: true,
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(absValue);
  }

  const fullPrecisionStr = absValue.toFixed(20).replace(/\.?0+$/, '');
  const [integerPart, decimalPart] = fullPrecisionStr.split('.');
  
  if (!decimalPart) {
    return `${sign}${integerPart}`;
  }

  if (decimalPart[0] !== '0') {
    return `${sign}${new Intl.NumberFormat('en-US', {
      useGrouping: true,
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(absValue)}`;
  }
  
  let nonZeroCount = 0;
  let lastIndex = -1;

  for (let i = 0; i < decimalPart.length; i++) {
    if (decimalPart[i] !== '0') {
      nonZeroCount += 1;
      lastIndex = i;
      if (nonZeroCount === 2) break;
    }
  }

  if (lastIndex === -1) {
    return `${sign}${integerPart}`;
  }

  const finalDecimalPart = decimalPart.slice(0, lastIndex + 1);
  const formattedValue = Number(`${integerPart}.${finalDecimalPart}`);

  return `${sign}${new Intl.NumberFormat('en-US', {
    useGrouping: true,
    minimumFractionDigits: 0,
    maximumFractionDigits: finalDecimalPart.length,
  }).format(formattedValue)}`;
}

export function formatPrice(
  value: unknown,
  options?: { accountType?: AccountType; fallbackFractionDigits?: number }
): string {
  const parsed = parseNumber(value);
  if (parsed === null) return String(value ?? '');

  const accountType = options?.accountType;
  const symbol = getCurrencySymbol(accountType);

  let formatted: string;
  
  if (accountType === 'crypto') {
    formatted = formatCryptoPrice(parsed);
  } else {
    const maximumFractionDigits = (() => {
      if (accountType === 'a_stock') return 2;
      if (accountType === 'us_stock' || accountType === 'hk_stock') return 2;
      return options?.fallbackFractionDigits ?? 2;
    })();

    formatted = new Intl.NumberFormat('en-US', {
      useGrouping: true,
      minimumFractionDigits: 0,
      maximumFractionDigits,
    }).format(parsed);
  }

  return `${symbol}${formatted}`;
}

export function formatQuantity(
  value: unknown,
  options?: { accountType?: AccountType; fallbackFractionDigits?: number }
): string {
  const parsed = parseNumber(value);
  if (parsed === null) return String(value ?? '');

  const accountType = options?.accountType;
  const maximumFractionDigits = (() => {
    if (accountType === 'a_stock') return 0;
    if (accountType === 'us_stock' || accountType === 'hk_stock') return 2;
    if (accountType === 'crypto') return options?.fallbackFractionDigits ?? 8;
    return options?.fallbackFractionDigits ?? 8;
  })();

  return new Intl.NumberFormat('en-US', {
    useGrouping: true,
    minimumFractionDigits: 0,
    maximumFractionDigits,
  }).format(parsed);
}
