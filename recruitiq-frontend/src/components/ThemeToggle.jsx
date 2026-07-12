import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../ThemeContext';

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isLight = theme === 'light';

  return (
    <button
      className="theme-toggle"
      onClick={toggleTheme}
      aria-label="Toggle light/dark theme"
      title={isLight ? 'Switch to dark mode' : 'Switch to light mode'}
    >
      <span className={`theme-toggle-thumb ${isLight ? 'is-light' : 'is-dark'}`}>
        {isLight ? <Sun size={13} /> : <Moon size={13} />}
      </span>
    </button>
  );
}
