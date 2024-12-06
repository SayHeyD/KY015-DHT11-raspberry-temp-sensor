<?php

namespace App\Http\Controllers;

use Inertia\Inertia;

class DashboardController extends Controller
{
    public function view()
    {
        return Inertia::render('Dashboard');
    }
}
