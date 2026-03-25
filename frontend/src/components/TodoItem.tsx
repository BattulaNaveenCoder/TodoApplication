import { useState, useCallback } from 'react';
import type { Todo, TodoUpdate } from '../types/todo';

interface TodoItemProps {
  todo: Todo;
  onToggleComplete: (todo: Todo) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onEdit: (id: number, data: TodoUpdate) => Promise<void>;
}

export function TodoItem({ todo, onToggleComplete, onDelete, onEdit }: TodoItemProps) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description ?? '');
  const [hovering, setHovering] = useState(false);

  const handleSave = useCallback(async () => {
    const trimmed = editTitle.trim();
    if (!trimmed) return;
    await onEdit(todo.id, {
      title: trimmed,
      description: editDescription.trim() || null,
    });
    setEditing(false);
  }, [editTitle, editDescription, todo.id, onEdit]);

  const handleCancel = useCallback(() => {
    setEditTitle(todo.title);
    setEditDescription(todo.description ?? '');
    setEditing(false);
  }, [todo.title, todo.description]);

  const formattedDate = new Date(todo.created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });

  if (editing) {
    return (
      <div className="group rounded-xl border border-indigo-200 bg-indigo-50/50 p-4 space-y-3">
        <input
          type="text"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          maxLength={200}
          className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-800 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-all"
          aria-label="Edit title"
          autoFocus
        />
        <textarea
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          maxLength={1000}
          rows={2}
          className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 resize-none transition-all"
          aria-label="Edit description"
        />
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={handleCancel}
            className="rounded-lg px-3 py-1.5 text-xs font-medium text-gray-500 hover:bg-gray-200/60 transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={!editTitle.trim()}
            className="rounded-lg bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white hover:bg-indigo-700 disabled:opacity-40 transition-all"
          >
            Save
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`group flex items-start gap-3 rounded-xl border p-4 transition-all ${
        todo.is_completed
          ? 'border-gray-100 bg-gray-50/50'
          : 'border-gray-100 bg-white hover:shadow-sm hover:border-gray-200'
      }`}
      onMouseEnter={() => setHovering(true)}
      onMouseLeave={() => setHovering(false)}
    >
      {/* Checkbox */}
      <button
        type="button"
        onClick={() => void onToggleComplete(todo)}
        className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-all ${
          todo.is_completed
            ? 'border-emerald-500 bg-emerald-500'
            : 'border-gray-300 hover:border-indigo-400'
        }`}
        aria-label={`Mark "${todo.title}" as ${todo.is_completed ? 'incomplete' : 'complete'}`}
      >
        {todo.is_completed && (
          <svg className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-medium leading-snug ${
          todo.is_completed ? 'text-gray-400 line-through' : 'text-gray-800'
        }`}>
          {todo.title}
        </p>
        {todo.description && (
          <p className={`mt-0.5 text-xs leading-relaxed ${
            todo.is_completed ? 'text-gray-300' : 'text-gray-500'
          }`}>
            {todo.description}
          </p>
        )}
        <p className="mt-1.5 text-[10px] font-medium uppercase tracking-wider text-gray-400">
          {formattedDate}
        </p>
      </div>

      {/* Actions */}
      <div
        className={`flex shrink-0 items-center gap-1 transition-opacity ${
          hovering ? 'opacity-100' : 'opacity-0'
        }`}
      >
        <button
          type="button"
          onClick={() => setEditing(true)}
          className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
          aria-label="Edit todo"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
          </svg>
        </button>
        <button
          type="button"
          onClick={() => void onDelete(todo.id)}
          className="rounded-lg p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-500 transition-colors"
          aria-label="Delete todo"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </div>
    </div>
  );
}
