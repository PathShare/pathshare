import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TripSearchComponent } from './trip-search.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [TripSearchComponent],
  exports: [TripSearchComponent]
})
export class TripSearchModule { }
