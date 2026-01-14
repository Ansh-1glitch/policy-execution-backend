/**
 * Backend API Integration Layer
 * 
 * This file provides functions to interact with the policy execution backend.
 * Copy this file to your ROCKET frontend project (e.g., src/api/ or src/services/)
 */

// Backend Configuration
const BACKEND_URL = "https://policy-execution-backend.onrender.com";
// For local development, uncomment:
// const BACKEND_URL = "http://localhost:8000";

// Type Definitions
export interface Task {
    task_id: string;
    policy_id: string;
    rule_id: string;
    task_name: string;
    assigned_role: string;
    status: "CREATED" | "ASSIGNED" | "IN_PROGRESS" | "COMPLETED" | "ESCALATED";
    deadline: string;
}

export interface AuditLog {
    task_id: string;
    action: string;
    performed_by_role: string;
    timestamp: string;
}

export interface UpdateStatusRequest {
    new_status: "ASSIGNED" | "IN_PROGRESS" | "COMPLETED" | "ESCALATED";
    role: string;
}

// API Functions

/**
 * Fetch tasks from backend, optionally filtered by role
 * @param role - Optional role filter (e.g., "Clerk", "Officer", "Admin")
 * @returns Array of tasks
 */
export async function fetchTasks(role?: string): Promise<Task[]> {
    try {
        const url = role
            ? `${BACKEND_URL}/tasks?role=${encodeURIComponent(role)}`
            : `${BACKEND_URL}/tasks?role=Admin`; // Default to Admin to see all tasks

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
        }

        const tasks: Task[] = await response.json();
        return tasks;
    } catch (error) {
        console.error('Error fetching tasks:', error);
        throw error;
    }
}

/**
 * Update task status
 * @param taskId - Task ID to update
 * @param newStatus - New status to set
 * @param role - Role of the user performing the action
 * @returns Updated task
 */
export async function updateTaskStatus(
    taskId: string,
    newStatus: "ASSIGNED" | "IN_PROGRESS" | "COMPLETED" | "ESCALATED",
    role: string
): Promise<Task> {
    try {
        const response = await fetch(`${BACKEND_URL}/tasks/${taskId}/update-status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                new_status: newStatus,
                role: role
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Failed to update task status: ${response.status}`);
        }

        const updatedTask: Task = await response.json();
        return updatedTask;
    } catch (error) {
        console.error('Error updating task status:', error);
        throw error;
    }
}

/**
 * Escalate a task to the next role level
 * @param taskId - Task ID to escalate
 * @param role - Role of the user performing the escalation
 * @returns Updated task
 */
export async function escalateTask(taskId: string, role: string): Promise<Task> {
    try {
        const response = await fetch(`${BACKEND_URL}/tasks/${taskId}/escalate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ role }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Failed to escalate task: ${response.status}`);
        }

        const updatedTask: Task = await response.json();
        return updatedTask;
    } catch (error) {
        console.error('Error escalating task:', error);
        throw error;
    }
}

/**
 * Check backend health
 * @returns Health status
 */
export async function checkBackendHealth(): Promise<{ status: string }> {
    try {
        const response = await fetch(`${BACKEND_URL}/`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`Backend health check failed: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error checking backend health:', error);
        throw error;
    }
}

/**
 * Get statistics for dashboard
 * @param role - Optional role filter
 * @returns Statistics object
 */
export async function getTaskStatistics(role?: string): Promise<{
    total: number;
    created: number;
    assigned: number;
    inProgress: number;
    completed: number;
    escalated: number;
}> {
    try {
        const tasks = await fetchTasks(role);

        return {
            total: tasks.length,
            created: tasks.filter(t => t.status === 'CREATED').length,
            assigned: tasks.filter(t => t.status === 'ASSIGNED').length,
            inProgress: tasks.filter(t => t.status === 'IN_PROGRESS').length,
            completed: tasks.filter(t => t.status === 'COMPLETED').length,
            escalated: tasks.filter(t => t.status === 'ESCALATED').length,
        };
    } catch (error) {
        console.error('Error getting task statistics:', error);
        throw error;
    }
}

// Export backend URL for direct access if needed
export { BACKEND_URL };
