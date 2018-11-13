import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { TripSearchModule } from './trip-search/trip-search.module';

import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { SignupComponent } from './auth/signup/signup.component';
import { SigninComponent } from './auth/signin/signin.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from './auth/auth.service';
import { ShareMyTripService } from './share-my-trip/share-my-trip.service';

//Kien: popup dependencies
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ShareMyTripComponent } from './share-my-trip/share-my-trip.component'




@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SignupComponent,
    SigninComponent,
    ShareMyTripComponent
  ],
  imports: [
    BrowserModule,
    TripSearchModule,
    HttpClientModule,
    //Kien: for signup comp
    FormsModule,
    //Kien: for signin popup
    NgbModule,
    ReactiveFormsModule,

    AppRoutingModule
  ],
  providers: [AuthService,ShareMyTripService],
  bootstrap: [AppComponent]
})
export class AppModule { }
