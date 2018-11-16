import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RideListingsComponent } from './ride-listings.component';

import {ReactiveFormsModule} from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  declarations: [RideListingsComponent],
  exports: [RideListingsComponent]
})
export class RideListingsModule { }
