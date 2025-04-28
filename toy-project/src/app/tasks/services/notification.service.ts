import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  alert(message: string) {
    console.log('Alert: ' + message);
  }
}
