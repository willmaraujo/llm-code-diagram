import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  getTasks() {
    return [{ id: 1, title: 'Sample Task' }];
  }

  getTask(id: number) {
    return { id, title: 'Sample Task ' + id };
  }
}
