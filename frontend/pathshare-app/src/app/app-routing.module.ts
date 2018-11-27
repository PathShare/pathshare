import { ViewProfileComponent } from './view-profile/view-profile.component';
import { TripSearchComponent } from './trip-search/trip-search.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SignupComponent } from './auth/signup/signup.component';
import { ShareMyTripComponent } from './share-my-trip/share-my-trip.component';
import { RideListingsComponent } from './ride-listings/ride-listings.component';

const appRoutes: Routes = [
  {path: '', redirectTo: 'trip-search', pathMatch: 'full'},
  {path: 'trip-search', component: TripSearchComponent },
  {path: 'rides', component: RideListingsComponent},
  {path: 'signup', component: SignupComponent },
  {path: 'share-my-trip', component: ShareMyTripComponent},
  {path: 'view-profile', component: ViewProfileComponent}

];

@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
