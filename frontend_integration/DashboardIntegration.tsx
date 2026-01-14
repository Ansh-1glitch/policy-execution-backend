/**
 * Dashboard Integration Example
 * 
 * This file shows how to integrate the backend API with your React dashboard.
 * Adapt this code to your existing DashboardInteractive.tsx component.
 */

import React, { useState, useEffect } from 'react';
import { fetchTasks, updateTaskStatus, escalateTask, getTaskStatistics, Task } from './api';

interface DashboardProps {
    currentUserRole: string; // "Clerk", "Officer", or "Admin"
}

export function DashboardInteractive({ currentUserRole }: DashboardProps) {
    // State Management
    const [tasks, setTasks] = useState<Task[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedRole, setSelectedRole] = useState<string>(currentUserRole);
    const [statistics, setStatistics] = useState({
        total: 0,
        created: 0,
        assigned: 0,
        inProgress: 0,
        completed: 0,
        escalated: 0,
    });

    // Load tasks when component mounts or role changes
    useEffect(() => {
        loadTasks();
    }, [selectedRole]);

    // Load tasks from backend
    async function loadTasks() {
        try {
            setIsLoading(true);
            setError(null);

            // Fetch tasks from backend
            const fetchedTasks = await fetchTasks(selectedRole);
            setTasks(fetchedTasks);

            // Calculate statistics
            const stats = await getTaskStatistics(selectedRole);
            setStatistics(stats);

        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load tasks');
            console.error('Error loading tasks:', err);
        } finally {
            setIsLoading(false);
        }
    }

    // Handle task status update
    async function handleUpdateStatus(taskId: string, newStatus: Task['status']) {
        try {
            // Update status on backend
            await updateTaskStatus(taskId, newStatus, currentUserRole);

            // Refresh tasks to show updated data
            await loadTasks();

            // Optional: Show success message
            console.log(`Task ${taskId} updated to ${newStatus}`);

        } catch (err) {
            alert(`Failed to update task: ${err instanceof Error ? err.message : 'Unknown error'}`);
            console.error('Error updating task:', err);
        }
    }

    // Handle task escalation
    async function handleEscalate(taskId: string) {
        try {
            // Escalate task on backend
            await escalateTask(taskId, currentUserRole);

            // Refresh tasks to show updated data
            await loadTasks();

            // Optional: Show success message
            console.log(`Task ${taskId} escalated`);

        } catch (err) {
            alert(`Failed to escalate task: ${err instanceof Error ? err.message : 'Unknown error'}`);
            console.error('Error escalating task:', err);
        }
    }

    // Determine available actions based on current status
    function getAvailableActions(task: Task): Array<{ label: string; status: Task['status'] }> {
        switch (task.status) {
            case 'CREATED':
                return [{ label: 'Assign', status: 'ASSIGNED' }];
            case 'ASSIGNED':
                return [{ label: 'Start', status: 'IN_PROGRESS' }];
            case 'IN_PROGRESS':
                return [
                    { label: 'Complete', status: 'COMPLETED' },
                    { label: 'Escalate', status: 'ESCALATED' },
                ];
            default:
                return [];
        }
    }

    // Render loading state
    if (isLoading) {
        return (
            <div className="dashboard-loading">
                <div className="spinner"></div>
                <p>Loading tasks...</p>
            </div>
        );
    }

    // Render error state
    if (error) {
        return (
            <div className="dashboard-error">
                <h3>Error Loading Tasks</h3>
                <p>{error}</p>
                <button onClick={loadTasks}>Retry</button>
            </div>
        );
    }

    // Main dashboard render
    return (
        <div className="dashboard">
            {/* Header */}
            <header className="dashboard-header">
                <h1>Policy Execution Dashboard</h1>
                <div className="role-selector">
                    <label>View as:</label>
                    <select
                        value={selectedRole}
                        onChange={(e) => setSelectedRole(e.target.value)}
                    >
                        <option value="Clerk">Clerk</option>
                        <option value="Officer">Officer</option>
                        <option value="Admin">Admin</option>
                    </select>
                </div>
                <button onClick={loadTasks} className="refresh-button">
                    🔄 Refresh
                </button>
            </header>

            {/* Statistics Overview */}
            <div className="statistics-grid">
                <div className="stat-card">
                    <h3>Total Tasks</h3>
                    <p className="stat-value">{statistics.total}</p>
                </div>
                <div className="stat-card">
                    <h3>Created</h3>
                    <p className="stat-value">{statistics.created}</p>
                </div>
                <div className="stat-card">
                    <h3>In Progress</h3>
                    <p className="stat-value">{statistics.inProgress}</p>
                </div>
                <div className="stat-card">
                    <h3>Completed</h3>
                    <p className="stat-value">{statistics.completed}</p>
                </div>
            </div>

            {/* Tasks List */}
            <div className="tasks-section">
                <h2>Tasks ({tasks.length})</h2>

                {tasks.length === 0 ? (
                    <div className="no-tasks">
                        <p>No tasks found for {selectedRole}</p>
                    </div>
                ) : (
                    <div className="tasks-grid">
                        {tasks.map((task) => (
                            <div key={task.task_id} className={`task-card status-${task.status.toLowerCase()}`}>
                                <div className="task-header">
                                    <h3>{task.task_name}</h3>
                                    <span className={`status-badge ${task.status.toLowerCase()}`}>
                                        {task.status}
                                    </span>
                                </div>

                                <div className="task-details">
                                    <p><strong>Policy:</strong> {task.policy_id}</p>
                                    <p><strong>Rule:</strong> {task.rule_id}</p>
                                    <p><strong>Assigned to:</strong> {task.assigned_role}</p>
                                    <p><strong>Deadline:</strong> {task.deadline}</p>
                                </div>

                                <div className="task-actions">
                                    {getAvailableActions(task).map((action) => (
                                        <button
                                            key={action.label}
                                            onClick={() => {
                                                if (action.label === 'Escalate') {
                                                    handleEscalate(task.task_id);
                                                } else {
                                                    handleUpdateStatus(task.task_id, action.status);
                                                }
                                            }}
                                            className={`action-button ${action.label.toLowerCase()}`}
                                        >
                                            {action.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default DashboardInteractive;
