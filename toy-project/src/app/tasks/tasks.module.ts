import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TaskListComponent } from './task-list/task-list.component';
import { TaskItemComponent } from './task-item/task-item.component';
import { TaskDetailsComponent } from './task-details/task-details.component';

@NgModule({
  declarations: [TaskListComponent, TaskItemComponent, TaskDetailsComponent],
  imports: [CommonModule],
})
export class TasksModule {}
