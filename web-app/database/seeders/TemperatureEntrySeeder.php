<?php

namespace Database\Seeders;

use App\Models\TemperatureEntry;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class TemperatureEntrySeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        TemperatureEntry::factory()
            ->count(300)
            ->create();
    }
}
