import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TodoList } from './TodoList';
import type { Todo } from '../types/todo';

const sampleTodos: Todo[] = [
  {
    id: 1,
    title: 'First todo',
    description: 'Description 1',
    is_completed: false,
    created_at: '2025-01-15T10:00:00Z',
    updated_at: '2025-01-15T10:00:00Z',
  },
  {
    id: 2,
    title: 'Second todo',
    description: null,
    is_completed: true,
    created_at: '2025-01-16T12:00:00Z',
    updated_at: '2025-01-16T12:00:00Z',
  },
];

const defaultProps = () => ({
  todos: [] as Todo[],
  isLoading: false,
  error: null as string | null,
  onToggleComplete: vi.fn().mockResolvedValue(undefined),
  onDelete: vi.fn().mockResolvedValue(undefined),
  onEdit: vi.fn().mockResolvedValue(undefined),
});

beforeEach(() => {
  vi.resetAllMocks();
});

describe('TodoList', () => {
  it('should show loading spinner when isLoading is true', () => {
    const props = defaultProps();
    props.isLoading = true;

    render(<TodoList {...props} />);

    expect(screen.getByText(/loading your todos/i)).toBeInTheDocument();
  });

  it('should show error message when error is provided', () => {
    const props = defaultProps();
    props.error = 'Something went wrong';

    render(<TodoList {...props} />);

    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  });

  it('should show empty state when todos array is empty', () => {
    render(<TodoList {...defaultProps()} />);

    expect(screen.getByText(/no todos yet/i)).toBeInTheDocument();
    expect(screen.getByText(/create your first todo/i)).toBeInTheDocument();
  });

  it('should render all todo items when todos are provided', () => {
    const props = defaultProps();
    props.todos = sampleTodos;

    render(<TodoList {...props} />);

    expect(screen.getByText('First todo')).toBeInTheDocument();
    expect(screen.getByText('Second todo')).toBeInTheDocument();
  });

  it('should not show loading or error when displaying todos', () => {
    const props = defaultProps();
    props.todos = sampleTodos;

    render(<TodoList {...props} />);

    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/no todos yet/i)).not.toBeInTheDocument();
  });

  it('should prioritize loading state over error and empty states', () => {
    const props = defaultProps();
    props.isLoading = true;
    props.error = 'Some error';

    render(<TodoList {...props} />);

    expect(screen.getByText(/loading your todos/i)).toBeInTheDocument();
    expect(screen.queryByText('Some error')).not.toBeInTheDocument();
  });

  it('should prioritize error state over empty state', () => {
    const props = defaultProps();
    props.error = 'Failed to load';

    render(<TodoList {...props} />);

    expect(screen.getByText('Failed to load')).toBeInTheDocument();
    expect(screen.queryByText(/no todos yet/i)).not.toBeInTheDocument();
  });
});
