import { TripSearchComponent } from './trip-search/trip-search.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SignupComponent } from './auth/signup/signup.component';

const appRoutes: Routes = [
  {path: '', redirectTo: 'trip-search', pathMatch:'full'},
  {path: 'trip-search', component: TripSearchComponent },
  {path: 'signup', component: SignupComponent }
];

@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }