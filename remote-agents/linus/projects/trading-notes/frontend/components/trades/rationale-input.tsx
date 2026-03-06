import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';

interface RationaleInputProps {
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  className?: string;
}

export function RationaleInput({
  value,
  onChange,
  placeholder = '请输入操作理由 (支持 Markdown)',
  label = '操作理由',
  className
}: RationaleInputProps) {
  return (
    <div className={`space-y-2 ${className || ''}`}>
      <Label htmlFor="rationale-input" className="text-sm font-medium">
        {label}
      </Label>
      <Textarea
        id="rationale-input"
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        rows={4}
        className="font-mono text-sm resize-y"
      />
      <p className="text-xs text-muted-foreground">
        提示: 记录你的交易决策依据，比如技术指标、基本面因素、市场情绪等
      </p>
    </div>
  );
}
