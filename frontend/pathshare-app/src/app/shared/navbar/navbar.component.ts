import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  // Page element displays. These will be updated based on routing information.
  displayPageTitle = true;
  displayBackButton = false;
  displayMenuIcons = true;

  constructor(
    private location: Location,
    private router: Router) { }

  ngOnInit() {
    // Check for navigation actions to set navbar element visibilities. If we've
    // navigated to a new page, check whether we are on the root page or not and
    // set title and icons accordingly.
    this.router.events.subscribe((event) => {
      if (event.constructor.name === 'NavigationStart') {
        if (event['url'] === '/') {
          // We are on the root page.
          this.displayPageTitle = true;
          this.displayBackButton = false;
          this.displayMenuIcons = true;
        } else {
          this.displayPageTitle = false;
          this.displayBackButton = true;
          this.displayMenuIcons = true;
        }
      }
    });
  }

  navigateBack() {
    this.location.back();
  }

}
