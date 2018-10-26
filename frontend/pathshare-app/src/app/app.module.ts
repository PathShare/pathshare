import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { TripSearchModule } from './trip-search/trip-search.module';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    TripSearchModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
