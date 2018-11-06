import { NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import {LoginComponent} from './login.component';
import { DialogsModule } from '@progress/kendo-angular-dialog';
import {ReactiveFormsModule} from '@angular/forms';
import { ButtonsModule } from '@progress/kendo-angular-buttons';
import {

  MatFormFieldModule, MatInputModule,

} from '@angular/material';



@NgModule({
  imports: [
    CommonModule,
    MatFormFieldModule,
    ReactiveFormsModule, 
    DialogsModule,
    MatInputModule
  ],
  declarations: [LoginComponent],
  exports: [LoginComponent,MatFormFieldModule,],
})
export class LoginModule { }