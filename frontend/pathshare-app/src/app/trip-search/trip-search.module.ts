import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TripSearchComponent } from './trip-search.component';

import {ReactiveFormsModule} from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  declarations: [TripSearchComponent],
  exports: [TripSearchComponent],
})
export class TripSearchModule { }
