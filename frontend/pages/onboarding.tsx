import Head from 'next/head'
import Link from 'next/link'

export default function Onboarding() {
  return (
    <>
      <Head>
        <title>Nail&apos;d Early Onboarding</title>
        <meta name="description" content="Join Nail'd as a featured nail tech" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white">
        {/* Header Section with Cream Background */}
        <div className="relative overflow-hidden" style={{ backgroundColor: '#FEFAE0' }}>
          {/* Background Circles */}
          <div className="absolute top-0 right-0 pointer-events-none">
            {/* Top circle */}
            <div className="w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 border border-gray-400 rounded-full opacity-30" 
                 style={{ transform: 'translate(50%, -50%)' }}></div>
          </div>
          <div className="absolute top-64 md:top-80 lg:top-96 right-0 pointer-events-none">
            {/* Bottom circle */}
            <div className="w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 border border-gray-400 rounded-full opacity-30" 
                 style={{ transform: 'translate(50%, -25%)' }}></div>
          </div>

          {/* Navigation */}
          <nav className="relative z-10 pt-8 px-6 sm:px-12 md:px-16 lg:px-24">
            <Link href="/" className="text-black hover:text-gray-600 transition-colors pp-eiko text-lg">
              ← Back to Home
            </Link>
          </nav>

          {/* Header */}
          <div className="relative z-10 container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pt-12 pb-16">
            <div className="max-w-4xl mx-auto text-left">
              <h1 className="text-6xl sm:text-7xl md:text-8xl font-medium text-black mb-4 pp-eiko leading-tight">
                Nail&apos;d Early<br />
                Onboarding
              </h1>
              {/* Horizontal line under header */}
              <div className="w-full h-px bg-gray-400 mt-8 opacity-50"></div>
            </div>
          </div>
        </div>

        {/* White Content Section */}
        <div className="bg-white">
          <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pb-24">
            {/* Main Content */}
            <div className="max-w-4xl mx-auto">
              {/* You Do Fire Nails Section */}
              <div className="text-center mb-16 pt-16">
                <h2 className="text-3xl sm:text-4xl font-medium text-black mb-8 pp-eiko">
                  You Do Fire Nails. We Bring the Clients.
                </h2>
                
                <div className="w-24 h-px bg-black mx-auto mb-8"></div>
                
                <div className="mb-12">
                  <h3 className="text-2xl font-medium text-black mb-6 pp-eiko">
                    What is Nail&apos;d?
                  </h3>
                  <p className="text-base leading-relaxed text-black max-w-3xl mx-auto font-inter">
                    Nail&apos;d connects nail techs and salons with local clients—and we do it based on style, not reviews or price. 
                    Our platform puts your designs front and center. Clients upload photos of the nails they want, and we 
                    match them to techs who bring that vision to life. We hype your work, build your brand, and send you 
                    clients who love your artistry.
                  </p>
                </div>
              </div>

              {/* What You Get Section */}
              <div className="text-center mb-16">
                <h3 className="text-2xl font-medium text-black mb-8 pp-eiko">
                  What You Get:
                </h3>
                
                <div className="space-y-4 max-w-2xl mx-auto">
                  <p className="text-base text-black font-inter">A free personal profile to showcase your best sets</p>
                  <p className="text-base text-black font-inter">Local marketing—without lifting a finger</p>
                  <p className="text-base text-black font-inter">100% of what you charge (we don&apos;t take a cut!)</p>
                  <p className="text-base text-black font-inter">Bookings from clients who know your style already</p>
                  <p className="text-base text-black font-inter">Featured on our TikTok & IG with 101K+ reach</p>
                </div>
                
                <p className="text-sm text-black mt-8 font-inter italic">
                  You&apos;re always in control. Set your services, prices, and schedule. We just bring more heat to your business.
                </p>
              </div>

              {/* Who It's For Section */}
              <div className="text-center mb-16">
                <h3 className="text-2xl font-medium text-black mb-8 pp-eiko">
                  Who It&apos;s For?
                </h3>
                
                <div className="space-y-4 max-w-2xl mx-auto">
                  <p className="text-base text-black font-inter">Salon techs ready to grow their client list</p>
                  <p className="text-base text-black font-inter">Independent techs building a name</p>
                  <p className="text-base text-black font-inter">
                    Anyone who does 
                    <span className="inline-block mx-1">
                      <span className="text-yellow-600">🔥</span>
                    </span>
                    nails and wants to get booked—not ghosted
                  </p>
                </div>
              </div>

              {/* Let Us Work For You Section */}
              <div className="text-center mb-16">
                <h3 className="text-2xl font-medium text-black mb-8 pp-eiko">
                  Let Us Work For You
                </h3>
                
                <div className="space-y-2 max-w-2xl mx-auto mb-8">
                  <p className="text-base text-black font-inter font-semibold">Your only job? Do great nails.</p>
                  <p className="text-base text-black font-inter">Our job? Drive clients, build your brand, and keep the schedule full.</p>
                </div>
              </div>

              {/* Apply Section */}
              <div className="text-center">
                <a 
                  href="https://docs.google.com/forms/u/0/d/e/1FAIpQLSemOSo_bHNsNIrRGnyu7RuK4hHY6-7tKClHGwEy6xirEGLycA/viewform?usp=header&pli=1"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center hover:text-gray-600 transition-colors cursor-pointer"
                >
                  <h3 className="text-2xl font-medium text-black mb-8 pp-eiko flex items-center justify-center">
                    <span className="mr-2">💫</span>
                    Apply to Be a Featured Tech:
                  </h3>
                </a>
                
                {/* QR Code */}
                <div className="flex justify-center mb-8">
                  <a 
                    href="https://docs.google.com/forms/u/0/d/e/1FAIpQLSemOSo_bHNsNIrRGnyu7RuK4hHY6-7tKClHGwEy6xirEGLycA/viewform?usp=header&pli=1"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block hover:opacity-80 transition-opacity cursor-pointer"
                  >
                    <img 
                      src="/naild_qrcode.png" 
                      alt="QR Code to apply as featured tech"
                      className="w-48 h-48 border-2 border-gray-300 rounded-lg"
                    />
                  </a>
                </div>
                
                <p className="text-sm text-gray-600 font-inter">
                  Scan QR code to apply or visit our application form
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}