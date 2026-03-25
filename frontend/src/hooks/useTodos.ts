import { useCallback, useEffect, useState } from 'react';
import type { Todo, TodoCreate, TodoUpdate } from '../types/todo';
import * as todosApi from '../api/todosApi';

interface UseTodosReturn {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;
  addTodo: (data: TodoCreate) => Promise<void>;
  editTodo: (id: number, data: TodoUpdate) => Promise<void>;
  removeTodo: (id: number) => Promise<void>;
  toggleComplete: (todo: Todo) => Promise<void>;
  refresh: () => Promise<void>;
}

export function useTodos(): UseTodosReturn {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await todosApi.fetchTodos();
      setTodos(data);
    } catch {
      setError('Failed to load todos');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const addTodo = useCallback(async (data: TodoCreate) => {
    const created = await todosApi.createTodo(data);
    setTodos((prev) => [created, ...prev]);
  }, []);

  const editTodo = useCallback(async (id: number, data: TodoUpdate) => {
    const updated = await todosApi.updateTodo(id, data);
    setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
  }, []);

  const removeTodo = useCallback(async (id: number) => {
    await todosApi.deleteTodo(id);
    setTodos((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toggleComplete = useCallback(async (todo: Todo) => {
    const updated = todo.is_completed
      ? await todosApi.uncompleteTodo(todo.id)
      : await todosApi.completeTodo(todo.id);
    setTodos((prev) => prev.map((t) => (t.id === todo.id ? updated : t)));
  }, []);

  return { todos, isLoading, error, addTodo, editTodo, removeTodo, toggleComplete, refresh };
}
