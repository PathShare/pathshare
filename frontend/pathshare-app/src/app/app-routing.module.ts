import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TripSearchComponent } from './trip-search/trip-search.component';
import { RideListingsComponent } from './ride-listings/ride-listings.component';

const routes: Routes = [
  { path: '', component: TripSearchComponent },
  { path: 'rides', component: RideListingsComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  declarations: [],
  exports: [RouterModule]
})
export class AppRoutingModule { }
