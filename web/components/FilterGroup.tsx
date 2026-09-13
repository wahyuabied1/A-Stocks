"use client";

interface Props<T extends string> {
  items: readonly T[];
  value: T;
  label: (value: T) => string;
  onChange: (value: T) => void;
  ariaLabel: string;
}

export default function FilterGroup<T extends string>({ items, value, label, onChange, ariaLabel }: Props<T>) {
  return (
    <div className="filters" role="group" aria-label={ariaLabel}>
      {items.map((item) => (
        <button key={item} type="button" aria-pressed={item === value} onClick={() => onChange(item)}>
          {label(item)}
        </button>
      ))}
    </div>
  );
}
