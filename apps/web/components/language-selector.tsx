export function LanguageSelector() {
  return (
    <select className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm text-ink" defaultValue="en">
      <option value="en">English</option>
      <option value="hi">Hindi</option>
      <option value="bn">Bengali</option>
    </select>
  );
}
