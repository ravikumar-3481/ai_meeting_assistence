import React from 'react';
import Navbar from '../common/Navbar';
import HeroSection from './HeroSection';
import FeaturesSection from './FeaturesSection';
import DemoSection from './DemoSection';
import TestimonialsSection from './TestimonialsSection';
import PricingSection from './PricingSection';
import Footer from '../common/Footer';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      <Navbar />
      <main className="flex-grow">
        <HeroSection />
        <FeaturesSection />
        <DemoSection />
        <TestimonialsSection />
      </main>
      <Footer />
    </div>
  );
}
