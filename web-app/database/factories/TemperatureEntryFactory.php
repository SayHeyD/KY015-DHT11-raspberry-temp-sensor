<?php

namespace Database\Factories;

use App\Models\Device;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\TemperatureEntry>
 */
class TemperatureEntryFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'device_id' => Device::all()->random()->id,
            'temperature' => $this->faker->randomFloat(2, -20, 50),
            'humidity' => $this->faker->randomFloat(2, 0, 100),
        ];
    }
}
