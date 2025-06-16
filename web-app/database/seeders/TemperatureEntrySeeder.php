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
        $dataPoints = 300;

        for ($i = 0; $i < $dataPoints; $i++) {

            $measured_at = now()->subMinutes($dataPoints - $i);

            TemperatureEntry::factory()
                ->create([
                    'measured_at' => $measured_at->toString()
                ]);
        }
    }
}
