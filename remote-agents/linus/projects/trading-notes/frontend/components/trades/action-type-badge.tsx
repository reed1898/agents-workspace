import { ActionType, ACTION_TYPE_CONFIG } from '@/types/trade';
import { Badge } from '@/components/ui/badge';

interface ActionTypeBadgeProps {
  type?: ActionType;
  className?: string;
}

export function ActionTypeBadge({ type, className }: ActionTypeBadgeProps) {
  if (!type) return null;

  const config = ACTION_TYPE_CONFIG[type];

  return (
    <Badge
      variant="outline"
      className={`inline-flex items-center gap-1 ${config.bgColor} ${config.color} border-0 ${className || ''}`}
    >
      <span>{config.icon}</span>
      <span>{config.label}</span>
    </Badge>
  );
}
