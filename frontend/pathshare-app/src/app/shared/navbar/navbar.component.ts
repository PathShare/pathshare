import { Component, OnInit } from '@angular/core';

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

  constructor() { }

  ngOnInit() {
  }

}
