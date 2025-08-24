import { useState, useRef } from 'react'
import Head from 'next/head'

interface NailTech {
  id: string
  name: string
  distance: string
  location: string
  rating: string
  image: string
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [currentSlide, setCurrentSlide] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const carouselRef = useRef<HTMLDivElement>(null)

  // Mock nail techs data - replace with real data later
  const mockNailTechs: NailTech[] = [
    {
      id: '1',
      name: 'Marissa',
      distance: '1.6 mi away',
      location: 'Richardson, TX',
      rating: '4.9',
      image: 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=400&h=400&fit=crop&crop=center'
    },
    {
      id: '2', 
      name: 'Jennifer',
      distance: '2.1 mi away',
      location: 'Plano, TX',
      rating: '4.9',
      image: 'https://images.unsplash.com/photo-1632345031435-8727f6897d53?w=400&h=400&fit=crop&crop=center'
    },
    {
      id: '3',
      name: 'Jennifer',
      distance: '2.1 mi away', 
      location: 'Plano, TX',
      rating: '4.9',
      image: 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=400&fit=crop&crop=center'
    },
    {
      id: '4',
      name: 'Jennifer',
      distance: '2.1 mi away',
      location: 'Plano, TX', 
      rating: '4.9',
      image: 'https://images.unsplash.com/photo-1583847645687-4770c01bec81?w=400&h=400&fit=crop&crop=center'
    },
    {
      id: '5',
      name: 'Jennifer',
      distance: '2.1 mi away',
      location: 'Plano, TX',
      rating: '4.9', 
      image: 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop&crop=center'
    }
  ]

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
  }

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault()
    const file = event.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleFindNailTech = () => {
    // Always prompt user to upload an image when button is clicked
    fileInputRef.current?.click()
  }

  const scrollCarousel = (direction: 'left' | 'right') => {
    if (carouselRef.current) {
      const cardWidth = 320 + 24 // card width + gap
      const scrollAmount = direction === 'left' ? -cardWidth : cardWidth
      carouselRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' })
    }
  }

  return (
    <>
      <Head>
        <title>Nail&apos;d - Find Your Perfect Nail Tech</title>
        <meta name="description" content="Find nail techs near you with similar work" />
        <link rel="icon" href="/favicon.ico" />

      </Head>

      <div className="min-h-screen" style={{ backgroundColor: '#FEFAE0' }}>
        <div className="container mx-auto px-24 pt-24 pb-12">
          <div className="text-center max-w-4xl mx-auto">
            <button 
              onClick={() => document.getElementById('giveaway')?.scrollIntoView({ behavior: 'smooth' })}
              className="inline-flex items-center px-4 py-2 bg-black bg-opacity-10 rounded-full text-sm text-black mb-8 hover:bg-opacity-20 transition-all duration-200 cursor-pointer"
            >
              <span>Want a free nail set? Contact us →</span>
            </button>
            <h2 className="text-4xl text-black mb-6 pp-eiko">Welcome to</h2>
            <h1 className="text-9xl font-medium text-black mb-12 pp-eiko leading-none">
              Nail&apos;d
            </h1>
            <div className="max-w-lg mx-auto mb-12">
              <p className="text-xl text-black leading-relaxed">
                Simply share a photo of your desired look, and we&apos;ll find the right nail tech near you to make it happen.
              </p>
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
            
            <button
              onClick={handleFindNailTech}
              disabled={isLoading}
              className="bg-black text-white py-4 px-8 rounded-full text-lg font-medium hover:bg-gray-800 transition-colors inline-flex items-center space-x-2 group"
            >
              <span>Find a nail tech</span>
              <svg className="w-5 h-5 transform group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
          </div>

          {/* Nails near you section */}
          <div className="mt-32">
            <h2 className="text-3xl font-medium text-black mb-4 pp-eiko">
              Nails near you:
            </h2>
            
            <div className="py-8">
              <div ref={carouselRef} className="flex space-x-6 overflow-x-auto pb-4 pt-4 scroll-smooth">
                {mockNailTechs.map((tech) => (
                  <div
                    key={tech.id}
                    className="flex-none w-80 bg-black rounded-2xl overflow-hidden cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="relative h-80">
                      <img
                        src={tech.image}
                        alt={tech.name}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute top-4 right-4 bg-black bg-opacity-60 text-white px-3 py-1 rounded-full text-sm flex items-center space-x-1">
                        <span>★</span>
                        <span>{tech.rating}</span>
                      </div>
                    </div>
                    <div className="p-6 text-white">
                      <h3 className="text-xl font-bold mb-2">{tech.name}</h3>
                      <p className="text-gray-300 text-sm">{tech.distance} | {tech.location}</p>
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Navigation arrows - moved below and aligned right */}
              <div className="flex justify-end space-x-2 mt-4">
                <button 
                  onClick={() => scrollCarousel('left')}
                  className="bg-white shadow-lg rounded-full p-3 hover:bg-gray-50 transition-colors"
                >
                  <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <button 
                  onClick={() => scrollCarousel('right')}
                  className="bg-white shadow-lg rounded-full p-3 hover:bg-gray-50 transition-colors"
                >
                  <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

        </div>
        
        {/* Giveaway Section - Full viewport height */}
        <div id="giveaway" className="bg-black text-white min-h-screen flex flex-col px-24 mt-20">
          <div className="flex-1 flex items-center justify-center">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-5xl font-medium text-white mb-8 pp-eiko">
                Want free nails?
              </h2>
              <p className="text-xl text-white leading-relaxed mb-12 max-w-3xl mx-auto">
                We&apos;re giving away a full set of nails to celebrate the launch of Nail&apos;d. Selected entries get free sets and a feature on Nail&apos;d! Apply below — 100% free
              </p>
              
              <div className="max-w-md mx-auto">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Instagram @"
                    className="w-full px-6 py-3 pr-20 rounded-full text-black text-lg focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                  />
                  <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black text-white px-6 py-2 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors">
                    Enter
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          {/* Footer */}
          <footer className="py-12 border-t border-gray-800">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                {/* Brand */}
                <div className="md:col-span-1">
                  <h3 className="text-2xl font-medium text-white mb-4 pp-eiko">Nail&apos;d</h3>
                  <p className="text-gray-400 text-sm">
                    Find your perfect nail tech with AI-powered visual search.
                  </p>
                </div>
                
                {/* Product */}
                <div>
                  <h4 className="text-white font-medium mb-4">Product</h4>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li><a href="#" className="hover:text-white transition-colors">Search</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Upload</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Browse</a></li>
                  </ul>
                </div>
                
                {/* Company */}
                <div>
                  <h4 className="text-white font-medium mb-4">Company</h4>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Press</a></li>
                  </ul>
                </div>
                
                {/* Support */}
                <div>
                  <h4 className="text-white font-medium mb-4">Support</h4>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                  </ul>
                </div>
              </div>
              
              {/* Bottom footer */}
              <div className="pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
                <p className="text-gray-400 text-sm">
                  © 2024 Nail&apos;d. All rights reserved.
                </p>
                <div className="flex space-x-6 mt-4 md:mt-0">
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <span className="sr-only">Instagram</span>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987s11.987-5.367 11.987-11.987C24.004 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.321-1.295L3.654 16.94c-.75-.75-.75-1.968 0-2.719l1.474-1.474c.806-.871 1.946-1.361 3.321-1.361 1.297 0 2.448.49 3.321 1.295l1.474 1.474c.75.75.75 1.968 0 2.719l-1.474 1.474c-.806.871-1.946 1.361-3.321 1.361z"/>
                    </svg>
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <span className="sr-only">Twitter</span>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </>
  )
} 