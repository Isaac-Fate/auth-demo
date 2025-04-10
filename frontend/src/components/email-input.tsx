import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { MailIcon } from "lucide-react";

interface EmailInputProps extends React.ComponentPropsWithoutRef<"input"> {}

export function EmailInput({ className, ...restProps }: EmailInputProps) {
  return (
    <div className="relative">
      <Input
        className={cn("peer pe-9", className)}
        placeholder="Email"
        type="email"
        {...restProps}
      />
      <div className="text-muted-foreground/80 pointer-events-none absolute inset-y-0 end-0 flex items-center justify-center pe-3 peer-disabled:opacity-50">
        <MailIcon size={16} aria-hidden="true" />
      </div>
    </div>
  );
}
