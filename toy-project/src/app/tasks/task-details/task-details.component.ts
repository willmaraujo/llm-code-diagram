import { Component } from '@angular/core';
import { TaskService } from '../services/task.service';
import { NotificationService } from '../services/notification.service';

@Component({
  selector: 'app-task-details',
  templateUrl: './task-details.component.html',
})
export class TaskDetailsComponent {
  task = this.taskService.getTask(1);
  constructor(
    private taskService: TaskService,
    private notificationService: NotificationService
  ) {}

  notify() {
    this.notificationService.alert('Task loaded!');
  }
}
