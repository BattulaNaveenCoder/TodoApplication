import { useTodos } from '../hooks/useTodos';
import { TodoForm } from '../components/TodoForm';
import { TodoList } from '../components/TodoList';

export function HomePage() {
  const { todos, isLoading, error, addTodo, editTodo, removeTodo, toggleComplete } = useTodos();

  const totalCount = todos.length;
  const completedCount = todos.filter((t) => t.is_completed).length;
  const pendingCount = totalCount - completedCount;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30">
      <div className="mx-auto max-w-2xl px-4 py-10 sm:py-16">
        {/* Header */}
        <div className="mb-10 text-center">
          <div className="inline-flex items-center justify-center h-14 w-14 rounded-2xl bg-indigo-600 shadow-lg shadow-indigo-200 mb-4">
            <svg className="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Todo App
          </h1>
          <p className="mt-2 text-sm text-gray-500">
            Stay organized and get things done.
          </p>

          {/* Stats */}
          {totalCount > 0 && (
            <div className="mt-5 inline-flex items-center gap-4 rounded-full bg-white px-5 py-2 shadow-sm border border-gray-100 text-xs font-medium">
              <span className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-indigo-500" />
                <span className="text-gray-600">{totalCount} total</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-amber-400" />
                <span className="text-gray-600">{pendingCount} pending</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                <span className="text-gray-600">{completedCount} done</span>
              </span>
            </div>
          )}
        </div>

        {/* Form */}
        <TodoForm onSubmit={addTodo} />

        {/* List */}
        <TodoList
          todos={todos}
          isLoading={isLoading}
          error={error}
          onToggleComplete={toggleComplete}
          onDelete={removeTodo}
          onEdit={editTodo}
        />

        {/* Footer */}
        <div className="mt-10 text-center text-xs text-gray-400">
          Built with FastAPI + React + Tailwind CSS
        </div>
      </div>
    </div>
  );
}
