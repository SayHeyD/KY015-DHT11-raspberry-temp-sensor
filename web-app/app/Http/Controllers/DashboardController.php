<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

class DashboardController extends Controller
{
    public function view()
    {
        $devices = Auth::user()->devices;

        return Inertia::render('Dashboard/View', [
            // 'devices' => [],
            'devices' => fn () => $devices->load([
                'temperatures' => function($query) {
                    $query
                        ->where('created_by', '>=', now()->subDay())
                        ->orderBy('created_at', 'desc');
                }
            ]),
        ]);
    }
}
