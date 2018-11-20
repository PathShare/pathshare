import { UserDataService } from './auth/user-data.service';
import { ViewProfileComponent } from './view-profile/view-profile.component';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { TripSearchModule } from './trip-search/trip-search.module';
import { RideListingsModule } from './ride-listings/ride-listings.module';

import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { SignupComponent } from './auth/signup/signup.component';
import { SigninComponent } from './auth/signin/signin.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from './auth/auth.service';
import { ShareMyTripService } from './share-my-trip/share-my-trip.service';

import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService } from './shared/in-memory-data-service';

//Kien: popup dependencies
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ShareMyTripComponent } from './share-my-trip/share-my-trip.component'




@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SignupComponent,
    SigninComponent,
    ViewProfileComponent,
    ShareMyTripComponent
  ],
  imports: [
    BrowserModule,
    TripSearchModule,
    HttpClientModule,
    RideListingsModule,
    //Kien: for signup comp
    FormsModule,
    //Kien: for signin popup
    NgbModule,
    ReactiveFormsModule,
    HttpClientInMemoryWebApiModule.forRoot(
      InMemoryDataService, { dataEncapsulation: false }
    )
    AppRoutingModule
  ],
  providers: [AuthService,ShareMyTripService,UserDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
