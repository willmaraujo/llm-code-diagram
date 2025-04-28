import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { RouterModule } from '@angular/router';
import { TasksModule } from './tasks/tasks.module';

@NgModule({
  declarations: [AppComponent, NavbarComponent],
  imports: [BrowserModule, TasksModule, RouterModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
