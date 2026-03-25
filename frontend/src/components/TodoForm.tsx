import { useState, useCallback } from 'react';
import type { FormEvent } from 'react';
import type { TodoCreate } from '../types/todo';

interface TodoFormProps {
  onSubmit: (data: TodoCreate) => Promise<void>;
}

export function TodoForm({ onSubmit }: TodoFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(false);

  const handleSubmit = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      const trimmed = title.trim();
      if (!trimmed) {
        setError('Title is required');
        return;
      }
      setError(null);
      setSubmitting(true);
      try {
        await onSubmit({
          title: trimmed,
          description: description.trim() || null,
        });
        setTitle('');
        setDescription('');
        setExpanded(false);
      } catch {
        setError('Failed to create todo');
      } finally {
        setSubmitting(false);
      }
    },
    [title, description, onSubmit],
  );

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mb-6 transition-all"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 border-dashed border-indigo-300">
          <svg className="h-3 w-3 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
        </div>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onFocus={() => setExpanded(true)}
          placeholder="Add a new todo..."
          maxLength={200}
          className="flex-1 text-sm text-gray-800 placeholder-gray-400 outline-none bg-transparent"
          aria-label="Todo title"
        />
      </div>

      {expanded && (
        <div className="mt-4 space-y-3 animate-in fade-in">
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add a description (optional)"
            maxLength={1000}
            rows={2}
            className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm text-gray-700 placeholder-gray-400 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 resize-none transition-all"
            aria-label="Todo description"
          />

          {error && (
            <p className="text-xs text-red-500 font-medium">{error}</p>
          )}

          <div className="flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={() => { setExpanded(false); setTitle(''); setDescription(''); setError(null); }}
              className="rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || !title.trim()}
              className="rounded-lg bg-indigo-600 px-5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all active:scale-[0.97]"
            >
              {submitting ? (
                <span className="flex items-center gap-2">
                  <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Adding...
                </span>
              ) : (
                'Add Todo'
              )}
            </button>
          </div>
        </div>
      )}
    </form>
  );
}
